using UnityEngine;

public class CrabeMovement : MonoBehaviour
{
    public float speed = 1f;
    private GameObject targetTurtle;

    void Update()
    {
        FindClosestTurtle();
        if (targetTurtle != null)
        {
            MoveTowardsTarget();
        }
    }

    void MoveTowardsTarget()
    {
        // Calculer la direction vers la tortue cible
        Vector3 targetDirection = (targetTurtle.transform.position - transform.position).normalized;

        // Orienter le crabe vers la tortue cible
        Quaternion targetRotation = Quaternion.LookRotation(targetDirection);
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * 5);

        // Se déplacer vers la tortue cible
        transform.position = Vector3.MoveTowards(transform.position, targetTurtle.transform.position, speed * Time.deltaTime);
    }

    void FindClosestTurtle()
    {
        GameObject[] turtles = GameObject.FindGameObjectsWithTag("Turtle");
        float closestDistance = Mathf.Infinity;
        GameObject closestTurtle = null;

        foreach (GameObject turtle in turtles)
        {
            float distance = Vector3.Distance(transform.position, turtle.transform.position);
            if (distance < closestDistance)
            {
                closestDistance = distance;
                closestTurtle = turtle;
            }
        }

        targetTurtle = closestTurtle;
    }

    private void OnCollisionEnter(Collision other)
    {
        if (other.gameObject.CompareTag("Turtle"))
        {
            GameObject turtleParent = other.transform.parent.gameObject; // Récupérer le parent de la tortue

            // Détruire la tortue
            Destroy(turtleParent); // Détruire le parent au lieu de l'objet enfant directement


            // Mettre à jour le score via le GameManager, si disponible
            if (GameGameManager.Instance != null)
            {
                //GameGameManager.Instance.AddScore(-1); // Retirer un point pour la destruction d'une tortue
                GameGameManager.Instance.LoseLife();
            }

            // Chercher la prochaine tortue la plus proche
            FindClosestTurtle();
        }
        // si c'est Wrist, détruire crabe
        if (other.gameObject.CompareTag("Wrist"))
        {
            Destroy(gameObject);
        }
    }
}
