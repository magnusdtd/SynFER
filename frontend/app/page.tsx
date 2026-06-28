"use client";

import React, { useState, useRef } from "react";
import { Header } from "../components/Header";
import { Footer } from "../components/Footer";
import { ToastAlert } from "../components/ToastAlert";
import { ReferenceUploadCard } from "../components/ReferenceUploadCard";
import { SynthesisCanvas } from "../components/SynthesisCanvas";
import { SynthesisController } from "../components/SynthesisController";
import { SynthesisActionsPanel } from "../components/SynthesisActionsPanel";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function Home() {
  // Core user states
  const [textPrompt, setTextPrompt] = useState<string>("");
  const [selectedFAUs, setSelectedFAUs] = useState<string[]>([]);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [stagedThumbnail, setStagedThumbnail] = useState<string | null>(null);

  // Output states
  const [generatedImageSrc, setGeneratedImageSrc] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [synthesisMetadata, setSynthesisMetadata] = useState<any>(null);

  // UX Assist states
  const [fauQuery, setFauQuery] = useState<string>("");
  const [activeFauCategory, setActiveFauCategory] = useState<string>("All");
  const [dragOverActive, setDragOverActive] = useState<boolean>(false);
  const [alertMessage, setAlertMessage] = useState<{ type: "success" | "warning" | "error"; text: string } | null>(null);

  // Node refs
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Helper flash alert
  const triggerAlert = (type: "success" | "warning" | "error", text: string) => {
    setAlertMessage({ type, text });
    setTimeout(() => {
      setAlertMessage(null);
    }, 5000);
  };

  // Drag & drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOverActive(true);
  };

  const handleDragLeave = () => {
    setDragOverActive(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOverActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processStagedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processStagedFile(e.target.files[0]);
    }
  };

  // Process and create browser preview
  const processStagedFile = (file: File) => {
    const validExtensions = ["image/png", "image/jpeg", "image/jpg"];
    if (!validExtensions.includes(file.type)) {
      triggerAlert("error", "Invalid format. Staged photos must be PNG or JPEG.");
      return;
    }
    
    setUploadedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setStagedThumbnail(e.target?.result as string);
    };
    reader.readAsDataURL(file);
    triggerAlert("success", `Staged reference configuration: ${file.name}`);
  };

  const removeStagedFile = () => {
    setUploadedFile(null);
    setStagedThumbnail(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    triggerAlert("warning", "Removed staged reference image.");
  };

  const handleClearAll = () => {
    setGeneratedImageSrc(null);
    setSynthesisMetadata(null);
    setTextPrompt("");
    setSelectedFAUs([]);
    setUploadedFile(null);
    setStagedThumbnail(null);
    triggerAlert("warning", "Synthesis stage reset.");
  };

  // Submit and synthethize expression
  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!uploadedFile) {
      triggerAlert("error", "A reference identity image is required.");
      return;
    }

    setIsLoading(true);

    try {
      // Build native FormData payload as specified
      const formData = new FormData();
      formData.append("prompt", textPrompt);
      formData.append("selectedFAUs", JSON.stringify(selectedFAUs));
      if (uploadedFile) {
        formData.append("uploadedFile", uploadedFile);
      }

      // Endpoint selection
      let fetchUrl = `/api/generate`;

      // Perform synthesis API call
      const response = await fetch(fetchUrl, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Synthesis backend returned status ${response.status}`);
      }

      const data = await response.json();

      if (data.image_b64) {
        setGeneratedImageSrc(`data:image/png;base64,${data.image_b64}`);
        if (data.metadata) {
          setSynthesisMetadata(data.metadata);
        } else {
          throw new Error("Synthesis metadata missing from backend response.");
        }
        triggerAlert("success", "Facial Expression Synthesized Successfully!");
      } else if (data.image_url) {
        setGeneratedImageSrc(data.image_url);
        if (data.metadata) {
          setSynthesisMetadata(data.metadata);
        } else {
          throw new Error("Synthesis metadata missing from backend response.");
        }
        triggerAlert("success", "Facial Expression Synthesized Successfully!");
      } else {
        throw new Error("No image URL returned from synthesis generator.");
      }
    } catch (err: any) {
      console.warn("Synthesis engine error:", err);
      triggerAlert("error", err.message || "Failed to contact synthesis engine.");
    } finally {
      setIsLoading(false);
    }
  };

  // Trigger file download helper
  const handleDownloadImage = async () => {
    if (!generatedImageSrc) return;
    
    try {
      const response = await fetch(generatedImageSrc);
      if (!response.ok) throw new Error("Failed to fetch image");
      
      const blob = await response.blob();
      const objectUrl = URL.createObjectURL(blob);
      
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = "synfer-synthesized-face.png";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(objectUrl);
      
      triggerAlert("success", "Saved synthesized artwork to downloads.");
    } catch (error) {
      console.error("Error downloading image:", error);
      triggerAlert("error", "Failed to download image directly. Opening in new tab instead.");
      window.open(generatedImageSrc, "_blank");
    }
  };

  return (
    <div id="synfer-root" className="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-indigo-600 selection:text-white flex flex-col">
      <ToastAlert alertMessage={alertMessage} />

      <Header />

      {/* Main Form & Grid Container */}
      <form id="synthesis-parameters-form" onSubmit={handleGenerate} className="w-full flex-1">
        <main id="synfer-main" className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1.4fr)_minmax(0,0.9fr)] lg:grid-rows-[minmax(0,1fr)_minmax(0,1fr)_auto] gap-4 p-4 max-w-[1600px] mx-auto h-[calc(100vh-80px)] min-h-0">
          
          <ReferenceUploadCard
            dragOverActive={dragOverActive}
            handleDragOver={handleDragOver}
            handleDragLeave={handleDragLeave}
            handleDrop={handleDrop}
            fileInputRef={fileInputRef}
            handleFileSelect={handleFileSelect}
            stagedThumbnail={stagedThumbnail}
            uploadedFile={uploadedFile}
            removeStagedFile={removeStagedFile}
          />

          <SynthesisCanvas
            generatedImageSrc={generatedImageSrc}
            isLoading={isLoading}
            synthesisMetadata={synthesisMetadata}
            selectedFAUs={selectedFAUs}
          />

          <SynthesisController
            textPrompt={textPrompt}
            setTextPrompt={setTextPrompt}
            selectedFAUs={selectedFAUs}
            setSelectedFAUs={setSelectedFAUs}
            fauQuery={fauQuery}
            setFauQuery={setFauQuery}
            activeFauCategory={activeFauCategory}
            setActiveFauCategory={setActiveFauCategory}
            triggerAlert={triggerAlert}
          />

          <SynthesisActionsPanel
            synthesisMetadata={synthesisMetadata}
            isLoading={isLoading}
            generatedImageSrc={generatedImageSrc}
            handleDownloadImage={handleDownloadImage}
            handleClearAll={handleClearAll}
          />

        </main>
      </form>

      <Footer />
    </div>
  );
}
