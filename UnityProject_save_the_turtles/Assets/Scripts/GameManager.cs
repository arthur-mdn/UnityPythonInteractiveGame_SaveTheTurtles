using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    public int Score { get; private set; } = 0;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        StartYoloDetection();
    }

    public void StartYoloDetection()
    {
    if (UdpConnectionManager.Instance != null)
        {
            UdpConnectionManager.Instance.SendData("start_yolo_hands_detection");
        }

    }

    public void ChangeToCalibrationScene()
    {
        SceneManager.LoadScene("BallGame");
    }

    public void LoadGameScene()
    {
        SceneManager.LoadScene("GameScene");
    }

    public void AddScore(int amount)
    {
        Score += amount;
        Debug.Log("Score: " + Score);
    }

    public int GetScore()
    {
        return Score;
    }
}