using UnityEngine;

public class TurtleMovement : MonoBehaviour
{
    private float minSpeed = 0.2f;
    private float maxSpeed = 0.8f;
    public float speed;
    private Quaternion targetRotation;

    void Start()
    {
        targetRotation = Quaternion.LookRotation(Vector3.right);
        speed = Random.Range(minSpeed, maxSpeed);
    }

    void Update()
    {
        if (GameGameManager.Instance.Gameover) return;
        transform.rotation = Quaternion.Lerp(transform.rotation, targetRotation, Time.deltaTime * 5);
        transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }
}
