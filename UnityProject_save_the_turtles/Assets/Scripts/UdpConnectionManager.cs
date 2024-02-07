// UdpConnectionManager.cs
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using SimpleJSON;
using System.Collections.Concurrent;
using UnityEngine.SceneManagement;

public class UdpConnectionManager : MonoBehaviour
{
    [SerializeField] private string IP = "127.0.0.1"; // local host
    [SerializeField] private int rxPort = 8000; // port to receive data from Python on
    [SerializeField] private int txPort = 8001; // port to send data to Python on

    public static UdpConnectionManager Instance;

    private UdpClient client;
    private IPEndPoint remoteEndPoint;
    private Thread receiveThread;
    
    private ConcurrentQueue<string> receivedMessages = new ConcurrentQueue<string>();

    private readonly Queue<Action> actionsToExecuteOnMainThread = new Queue<Action>();

    public void EnqueueMainThreadAction(Action action)
    {
        lock (actionsToExecuteOnMainThread)
        {
            actionsToExecuteOnMainThread.Enqueue(action);
        }
    }

    public GameObject connectingUI;
    public GameObject connectErrorUI;
    public GameObject connectOkUI;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
            remoteEndPoint = new IPEndPoint(IPAddress.Parse(IP), txPort);
            client = new UdpClient(rxPort);
            receiveThread = new Thread(new ThreadStart(ReceiveData));
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        if (!connectingUI) connectingUI = GameObject.Find("Connecting");
        if (!connectErrorUI) connectErrorUI = GameObject.Find("ConnectError");
        if (!connectOkUI) connectOkUI = GameObject.Find("ConnectOk");

        // Assurez-vous de désactiver ces UIs au démarrage
        if (connectingUI) connectingUI.SetActive(true);
        if (connectErrorUI) connectErrorUI.SetActive(false);
        if (connectOkUI) connectOkUI.SetActive(false);

        SendData("test_connection");
    }

    private void UpdateConnectionState(string state)
    {
        if (connectingUI) connectingUI.SetActive(state == "Connecting");
        if (connectErrorUI) connectErrorUI.SetActive(state == "ConnectError");
        if (connectOkUI) connectOkUI.SetActive(state == "ConnectOk");
    }



   void Update()
   {
       // Exécutez toutes les actions en attente sur le thread principal
       while (actionsToExecuteOnMainThread.Count > 0)
       {
           Action action;
           lock (actionsToExecuteOnMainThread)
           {
               action = actionsToExecuteOnMainThread.Dequeue();
           }
           action?.Invoke();
       }

       // Traitement des messages reçus
       while (receivedMessages.TryDequeue(out string message))
       {
           ProcessInput(message);
       }
   }
    
    public void SendData(string message)
    {
        SocketMessage socketMessage = new SocketMessage
        {
            sender = "unity",
            message = message,
            data = ""
        };

        string json = JsonUtility.ToJson(socketMessage);
        byte[] data = Encoding.UTF8.GetBytes(json);
        Debug.Log("Sending: " + json);
        client.Send(data, data.Length, remoteEndPoint);
    }

    private void ReceiveData()
    {
        try
        {
            while (true)
            {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                receivedMessages.Enqueue(text);
            }
        }
        catch (Exception e)
        {
            EnqueueMainThreadAction(() => UpdateConnectionState("ConnectError"));
        }
    }

    private void ProcessInput(string json)
    {
        var node = JSON.Parse(json);
        string messageType = node["message"];
//        Debug.Log(messageType);
        if (messageType == "connection_ok")
        {
            EnqueueMainThreadAction(() => UpdateConnectionState("ConnectOk"));
        }
        else if (messageType == "calibration_success")
        {
            SendData("start_detection");
            EnqueueMainThreadAction(ShowCalibrateOkTemporarily);
        }
        else if (messageType == "calibration_failed")
        {
            EnqueueMainThreadAction(ShowCalibrateFailedTemporarily);
        }
        else if (messageType == "hands_positions")
        {
            var positions = node["data"].AsArray;
            CalibrationManager.Instance.UpdateWristPositions(positions);
        }
        else if (messageType == "change_scene_to_calibrate")
        {
            SceneManager.LoadScene("BallGame");
        }
        else if (messageType == "game_stopped")
        {
            SceneManager.LoadScene("HomeScreen");
        }
        else if (messageType == "start_new_game")
        {
            SendData("start_detection");
            SceneManager.LoadScene("Game");
        }
    }

    void ShowCalibrateOkTemporarily()
    {
        ShowStartCalibration showStartCalibration = FindObjectOfType<ShowStartCalibration>();

        if (showStartCalibration != null)
        {
            showStartCalibration.StartCalibrateOkDisplay();
        }
        else
        {
            Debug.Log("ShowStartCalibration script non trouvé dans la scène.");
        }
    }
    void ShowCalibrateFailedTemporarily()
    {
        ShowStartCalibration showStartCalibration = FindObjectOfType<ShowStartCalibration>();

        if (showStartCalibration != null)
        {
            showStartCalibration.StartCalibrateFailedDisplay();
        }
        else
        {
            Debug.Log("ShowStartCalibration script non trouvé dans la scène.");
        }
    }
}


[Serializable]
public class SocketMessage
{
    public string sender;
    public string message;
    public string data;
}
