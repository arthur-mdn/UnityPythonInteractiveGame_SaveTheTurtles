using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    // Logique spécifique au jeu...

    public void LoadGameScene()
    {
        // Appelé après la calibration
        SceneManager.LoadScene("GameScene");
    }
}