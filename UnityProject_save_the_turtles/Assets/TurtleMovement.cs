using UnityEngine;

public class TurtleMovement : MonoBehaviour
{
    public float speed = 2f;

    void Start()
    {
        transform.rotation = Quaternion.LookRotation(Vector3.right);
    }

    void Update()
    {
        transform.Translate(Vector3.forward * speed * Time.deltaTime);
    }
}
