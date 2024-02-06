using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class StartCalibrationManager : MonoBehaviour
{
    void Start()
    {
        if (UdpConnectionManager.Instance != null)
        {
            UdpConnectionManager.Instance.SendData("start_yolo_hands_detection");
        }
    }
}
