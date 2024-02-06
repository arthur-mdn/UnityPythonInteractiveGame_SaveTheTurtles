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
//            DontDestroyOnLoad(gameObject);
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