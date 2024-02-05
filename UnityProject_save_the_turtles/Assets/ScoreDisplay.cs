using UnityEngine;
using TMPro; // Assurez-vous d'importer l'espace de noms pour TextMeshPro

public class ScoreDisplay : MonoBehaviour
{
    public TMP_Text scoreText; // Référence à l'élément TextMeshPro UI pour afficher le score

    private void Update()
    {
        if (GameGameManager.Instance != null) // Vérifiez si l'instance de GameGameManager existe
        {
            scoreText.text = "Score: " + GameGameManager.Instance.GetScore(); // Mettez à jour le texte du score
        }
    }
}
