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
            // Se déplacer vers la tortue cible
             Vector3 targetDirection = (targetTurtle.transform.position - transform.position).normalized;

            // Orienter le crabe vers la direction cible
            Quaternion targetRotation = Quaternion.LookRotation(targetDirection);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * 5);

            // Se déplacer vers la tortue cible
            transform.position = Vector3.MoveTowards(transform.position, targetTurtle.transform.position, speed * Time.deltaTime);

        }
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

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Turtle"))
        {
            Destroy(other.gameObject); // Détruire la tortue
            if (GameManager.Instance != null)
            {
                GameManager.Instance.AddScore(-1); // Retirer un point
            }
            Destroy(gameObject); // Détruire le crabe
        }
    }
}
