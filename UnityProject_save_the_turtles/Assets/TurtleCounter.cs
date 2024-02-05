using UnityEngine;

public class TurtleCounter : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Turtle"))
        {
            if (GameGameManager.Instance != null)
            {
                GameGameManager.Instance.AddScore(1);

                // Vérifie si l'objet tortue a un parent et détruit le parent
                if (other.transform.parent != null)
                {
                    Destroy(other.transform.parent.gameObject);
                }
                else
                {
                    // Si la tortue n'a pas de parent (pas logique), quand même détruire l'objet tortue directement
                    Destroy(other.gameObject);
                }
            }
            else
            {
                Debug.LogError("GameManager instance is null.");
            }
        }
    }
}
