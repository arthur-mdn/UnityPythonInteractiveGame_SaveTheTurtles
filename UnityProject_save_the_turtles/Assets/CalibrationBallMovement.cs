using UnityEngine;
using UnityEngine.SceneManagement;

public class CalibrationBallMovement : MonoBehaviour
{
    private Vector3 lastPosition;
    private float totalMovement = 0f; // Total de distance parcourue
    private float movementThreshold = 5f; // Seuil de mouvement pour déclencher le changement de scène
    private float checkInterval = 0.5f; // Intervalle de temps en secondes entre les vérifications

    void Start()
    {
        lastPosition = transform.position;
        InvokeRepeating(nameof(CheckMovement), checkInterval, checkInterval);
    }

    void CheckMovement()
    {
        float distanceMoved = Vector3.Distance(transform.position, lastPosition);
        totalMovement += distanceMoved;

        if (totalMovement >= movementThreshold)
        {
            LoadGameScene();
        }

        lastPosition = transform.position;
    }

    void LoadGameScene()
    {
        CancelInvoke(nameof(CheckMovement)); // Annuler les vérifications répétées avant de changer de scène
        SceneManager.LoadScene("Game");
    }
}
