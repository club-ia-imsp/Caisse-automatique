import React, { useRef, useEffect, useCallback, useState } from 'react';
import Webcam from 'react-webcam';
import { getWsUrl } from '../services/api';

const CameraFeed = ({ onDetections, onCartUpdate, isActive, setIsActive }) => {
  const webcamRef = useRef(null);
  const wsRef = useRef(null);
  const sendTimerRef = useRef(null);
  const waitingForResponse = useRef(false);
  const [annotatedFrame, setAnnotatedFrame] = useState(null);
  const [wsStatus, setWsStatus] = useState('disconnected');
  const [message, setMessage] = useState('');

  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(getWsUrl());
    
    ws.onopen = () => {
      setWsStatus('connected');
      setMessage('');
      waitingForResponse.current = false;
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Mark response received - allow sending next frame
        waitingForResponse.current = false;

        if (data.annotated_frame) {
          setAnnotatedFrame(`data:image/jpeg;base64,${data.annotated_frame}`);
        }
        
        if (data.detections) {
          onDetections(data.detections);
        }
        
        if (data.cart) {
          onCartUpdate(data.cart);
        }

        if (data.message) {
          setMessage(data.message);
        }
      } catch (e) {
        console.error('Error parsing WS message:', e);
        waitingForResponse.current = false;
      }
    };

    ws.onclose = () => {
      setWsStatus('disconnected');
      waitingForResponse.current = false;
    };

    ws.onerror = () => {
      setWsStatus('error');
      waitingForResponse.current = false;
    };

    wsRef.current = ws;
  }, [onDetections, onCartUpdate]);

  const sendFrame = useCallback(() => {
    if (!webcamRef.current || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
    
    // Don't send if still waiting for the previous response (back-pressure)
    if (waitingForResponse.current) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      waitingForResponse.current = true;
      wsRef.current.send(JSON.stringify({
        type: 'frame',
        data: imageSrc
      }));
    }
  }, []);

  useEffect(() => {
    if (isActive) {
      connectWebSocket();
      // Send frames at regular intervals, but sendFrame will skip if still waiting
      sendTimerRef.current = setInterval(sendFrame, 100);
    } else {
      if (sendTimerRef.current) {
        clearInterval(sendTimerRef.current);
        sendTimerRef.current = null;
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      setAnnotatedFrame(null);
      setWsStatus('disconnected');
      waitingForResponse.current = false;
    }

    return () => {
      if (sendTimerRef.current) clearInterval(sendTimerRef.current);
      if (wsRef.current) wsRef.current.close();
    };
  }, [isActive, connectWebSocket, sendFrame]);

  const statusColors = {
    connected: 'bg-primary',
    disconnected: 'bg-gray-400',
    error: 'bg-red-500'
  };

  const statusLabels = {
    connected: 'Connecté',
    disconnected: 'Déconnecté',
    error: 'Erreur'
  };

  return (
    <div className="flex flex-col h-full">
      {/* Status bar */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${statusColors[wsStatus]} ${wsStatus === 'connected' ? 'animate-pulse-green' : ''}`}></div>
          <span className="text-sm text-gray-600">{statusLabels[wsStatus]}</span>
        </div>
        <button
          onClick={() => setIsActive(!isActive)}
          className={`text-sm font-medium px-4 py-1.5 rounded-lg transition-all ${
            isActive
              ? 'bg-red-100 text-red-600 hover:bg-red-200'
              : 'bg-primary/10 text-primary hover:bg-primary/20'
          }`}
        >
          {isActive ? (
            <><i className="fa-solid fa-stop mr-1.5"></i>Arrêter</>
          ) : (
            <><i className="fa-solid fa-play mr-1.5"></i>Démarrer</>
          )}
        </button>
      </div>

      {/* Camera view */}
      <div className="relative flex-1 bg-gray-900 rounded-2xl overflow-hidden min-h-[250px] sm:min-h-[350px]">
        {isActive ? (
          <>
            {/* Live webcam feed always visible underneath */}
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              screenshotQuality={0.6}
              videoConstraints={{ facingMode: 'environment', width: 640, height: 480 }}
              className="absolute inset-0 w-full h-full object-cover"
            />
            
            {/* Annotated frame overlay on top of live feed */}
            {annotatedFrame && (
              <img
                src={annotatedFrame}
                alt="Detection"
                className="absolute inset-0 w-full h-full object-contain"
                style={{ zIndex: 1 }}
              />
            )}

            {/* Message overlay */}
            {message && (
              <div className="absolute bottom-4 left-4 right-4 bg-black/70 text-white text-sm py-2 px-4 rounded-lg">
                {message}
              </div>
            )}
          </>
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-white/70">
            <i className="fa-solid fa-video-slash text-4xl sm:text-5xl mb-4"></i>
            <p className="text-base sm:text-lg font-medium">Caméra inactive</p>
            <p className="text-xs sm:text-sm mt-1">Cliquez sur "Démarrer" pour commencer la détection</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CameraFeed;
