using UnityEngine;
using TMPro;

public class ScoreDisplay : MonoBehaviour
{
    public TMP_Text scoreText;

    private void Update()
    {
        if (GameGameManager.Instance != null)
        {
            scoreText.text = "Score: " + GameGameManager.Instance.GetScore();
        }
    }
}
