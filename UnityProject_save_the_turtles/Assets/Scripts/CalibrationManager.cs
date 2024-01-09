//CalibrationManager.cs
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using SimpleJSON; 
using System.Collections.Concurrent;


public class CalibrationManager : MonoBehaviour
{
    public GameObject wristPrefab; // Préfabriqué pour les poignets
    public GameObject planeGameObject;
    private List<GameObject> instantiatedWristPrefabs = new List<GameObject>(); // Liste pour stocker les instances
    public static CalibrationManager Instance { get; private set; }

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        Mesh mesh = planeGameObject.GetComponent<MeshFilter>().mesh;
        float planeWidth = mesh.bounds.size.x * planeGameObject.transform.localScale.x;
        float planeHeight = mesh.bounds.size.z * planeGameObject.transform.localScale.z;

        Debug.Log("Largeur du Plane: " + planeWidth);
        Debug.Log("Hauteur du Plane: " + planeHeight);
        UdpConnectionManager.Instance.SendData("start_calibration");

    }
    
    public void UpdateWristPositions(JSONArray handPositions)
    {
        ClearWristInstances();
        foreach (JSONNode pos in handPositions)
        {
            Vector3 worldPos = ConvertToPlanePosition(pos[0].AsFloat, pos[1].AsFloat);
            GameObject wristInstance = Instantiate(wristPrefab, worldPos, Quaternion.identity);
            instantiatedWristPrefabs.Add(wristInstance);
        }
    }
    
    private void ClearWristInstances()
    {
        foreach (GameObject wristInstance in instantiatedWristPrefabs)
        {
            Destroy(wristInstance); 
        }
        instantiatedWristPrefabs.Clear(); 
    }

    private Vector3 ConvertToPlanePosition(float x, float y)
    {
        Mesh mesh = planeGameObject.GetComponent<MeshFilter>().mesh;
        float planeWidth = mesh.bounds.size.x * planeGameObject.transform.localScale.x;
        float planeHeight = mesh.bounds.size.z * planeGameObject.transform.localScale.z;
        
        y = 1 - y;
        
        // Conversion des coordonnées
        float posX = (x * planeWidth) - (planeWidth / 2f);
        float posY = (y * planeHeight) - (planeHeight / 2f);

        return new Vector3(posX, 0.5f, posY);
    }

}

