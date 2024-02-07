using UnityEngine;
using TMPro;

public class ScoreDisplay : MonoBehaviour
{
    public TMP_Text scoreText;

    private void Update()
    {
        if (GameManager.Instance != null)
        {
            scoreText.text = "" + GameManager.Instance.GetScore();
        }
    }
}
