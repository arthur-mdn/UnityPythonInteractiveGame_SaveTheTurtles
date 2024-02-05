using UnityEngine;
using UnityEngine.SceneManagement;

public class GameGameManager : MonoBehaviour
{
    public static GameGameManager Instance { get; private set; }
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