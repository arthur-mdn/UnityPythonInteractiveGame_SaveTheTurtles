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

    void Update()
    {
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
        client.Send(data, data.Length, remoteEndPoint);
    }

    private void ReceiveData()
    {
        while (true)
        {
            IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
            byte[] data = client.Receive(ref anyIP);
            string text = Encoding.UTF8.GetString(data);
            receivedMessages.Enqueue(text); // Mettez les données reçues dans la file d'attente
        }
    }

    private void ProcessInput(string json)
    {
        var node = JSON.Parse(json);
        string messageType = node["message"];
//        Debug.Log(messageType);
        if (messageType == "calibration_success")
        {
            SendData("start_detection");
        }
        else if (messageType == "hands_positions")
        {
            var positions = node["data"].AsArray;
//            Debug.Log(positions);
            CalibrationManager.Instance.UpdateWristPositions(positions);
        }
        else if (messageType == "change_scene_to_calibrate")
        {
            GameManager.Instance.ChangeToCalibrationScene();
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
