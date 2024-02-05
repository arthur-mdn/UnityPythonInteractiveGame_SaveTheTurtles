using UnityEngine;
using UnityEngine.SceneManagement;

public class GameGameManager : MonoBehaviour
{
    public static GameGameManager Instance { get; private set; }
    public int Score { get; private set; } = 0;
    public int Lives { get; private set; } = 3;

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

     public void LoseLife()
    {
        Lives--;
        Debug.Log("Lives left: " + Lives);
        CheckGameOver();
    }

    public int GetScore()
    {
        return Score;
    }

     private void CheckGameOver()
    {
        if (Lives <= 0)
        {
            Debug.Log("Game Over!");
            Time.timeScale = 0;
        }
    }
}