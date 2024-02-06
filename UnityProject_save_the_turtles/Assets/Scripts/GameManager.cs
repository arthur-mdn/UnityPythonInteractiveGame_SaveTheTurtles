using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    public int Score { get; private set; } = 0;
    public int Lives { get; private set; } = 5;
    public bool Gameover { get; private set; } = false;
    public GameObject gameOverUI;

    public int GetLives() {
        return Lives;
    }

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
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
        LifeManager.Instance.UpdateLives(Lives);
        CheckGameOver();
    }

    public int GetScore()
    {
        return Score;
    }

     private void CheckGameOver()
     {
         if (Lives <= 0 && !Gameover)
         {
             Debug.Log("Game Over!");
             Gameover = true;
             gameOverUI.SetActive(true);
             StartCoroutine(WaitAndLoadHomeScreen(30)); // rediriger vers la page d'accueil après 30 secondes
             //Time.timeScale = 0;
         }
     }

     private IEnumerator WaitAndLoadHomeScreen(float delay)
     {
        yield return new WaitForSeconds(delay);
        UdpConnectionManager.Instance.SendData("stop_game");
     }
}