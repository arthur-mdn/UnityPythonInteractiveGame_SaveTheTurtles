using UnityEngine;

public class LifeManager : MonoBehaviour
{
    public static LifeManager Instance { get; private set; }

    public GameObject heartFullPrefab;
    public GameObject heartEmptyPrefab;
    public Transform heartsContainer;

    private GameObject[] heartsFull;
    private GameObject[] heartsEmpty;

    private void Awake()
    {
        if (Instance == null) {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        } else {
            Destroy(gameObject);
        }
    }

    private void Start() {
        InitializeHearts(GameGameManager.Instance.GetLives());
    }

    private void InitializeHearts(int maxLives)
    {
        heartsFull = new GameObject[maxLives];
        heartsEmpty = new GameObject[maxLives];

        Quaternion rotation = Quaternion.Euler(90f, 0f, 0f);

        for (int i = 0; i < maxLives; i++)
        {
            heartsFull[i] = Instantiate(heartFullPrefab, heartsContainer.position + Vector3.right * i * 0.5f, rotation, heartsContainer);

            heartsEmpty[i] = Instantiate(heartEmptyPrefab, heartsContainer.position + Vector3.right * i * 0.5f, rotation, heartsContainer);
            heartsEmpty[i].SetActive(false);
        }
    }

    public void UpdateLives(int currentLives)
    {
        for (int i = 0; i < heartsFull.Length; i++)
        {
            heartsFull[i].SetActive(i < currentLives);
            heartsEmpty[i].SetActive(i >= currentLives);
        }
    }
}
