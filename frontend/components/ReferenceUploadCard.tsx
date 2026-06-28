import React from "react";
import Image from "next/image";
import { Upload, X } from "lucide-react";

interface ReferenceUploadCardProps {
  dragOverActive: boolean;
  handleDragOver: (e: React.DragEvent) => void;
  handleDragLeave: () => void;
  handleDrop: (e: React.DragEvent) => void;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
  handleFileSelect: (e: React.ChangeEvent<HTMLInputElement>) => void;
  stagedThumbnail: string | null;
  uploadedFile: File | null;
  removeStagedFile: () => void;
}

export function ReferenceUploadCard({
  dragOverActive,
  handleDragOver,
  handleDragLeave,
  handleDrop,
  fileInputRef,
  handleFileSelect,
  stagedThumbnail,
  uploadedFile,
  removeStagedFile,
}: ReferenceUploadCardProps) {
  return (
    <section className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-2xl flex flex-col lg:col-span-1 lg:row-span-2 gap-3 h-full">
      <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-500 flex items-center gap-2">
        <Upload className="w-4 h-4 text-indigo-400" />
        Reference Identity Image
      </h2>
      
      <div className="flex-1 flex flex-col gap-4 min-h-0">
        <input
          type="file"
          id="uploaded-file-input"
          ref={fileInputRef}
          accept=".png, .jpg, .jpeg"
          onChange={handleFileSelect}
          className="hidden"
        />

        {/* Upload Action Drag zone */}
        {!stagedThumbnail && (
          <div
            id="drag-upload-zone"
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`flex-1 border-2 border-dashed hover:border-indigo-500/50 rounded-xl p-4 flex flex-col items-center justify-center bg-zinc-950 transition-colors cursor-pointer group min-h-[120px] ${
              dragOverActive
                ? "border-indigo-500 bg-indigo-950/25"
                : "border-zinc-800 hover:bg-zinc-900/10"
            }`}
          >
            <Upload className={`w-8 h-8 mb-3 transition ${dragOverActive ? "text-indigo-400" : "text-zinc-600 group-hover:text-indigo-400"}`} />
            <p className="text-sm text-zinc-400 font-bold mb-1 group-hover:text-zinc-300">Click or Drag Image</p>
            <p className="text-[10px] text-zinc-500 uppercase tracking-tighter">Drop Reference Here</p>
          </div>
        )}

        {/* Staging display preview */}
        {stagedThumbnail && (
          <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-3 flex flex-col gap-2 relative flex-1 min-h-0" onClick={(e) => e.stopPropagation()}>
            <div className="relative w-full flex-1 bg-zinc-800/50 rounded-lg border border-zinc-700 overflow-hidden group/preview min-h-0">
              <Image
                src={stagedThumbnail}
                alt="Staged Image Preview"
                fill
                className="object-contain"
                referrerPolicy="no-referrer"
              />
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  removeStagedFile();
                }}
                className="absolute top-2 right-2 bg-rose-500/90 hover:bg-rose-500 text-white p-1.5 rounded-full shadow-lg transition-transform hover:scale-105 active:scale-95 z-10"
                title="Clear image"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="w-full flex justify-between items-center shrink-0 mt-1">
              <div className="min-w-0 pr-2">
                <p className="text-xs text-zinc-300 truncate font-semibold leading-tight">
                  {uploadedFile?.name}
                </p>
                <p className="text-[10px] text-zinc-600 mt-1">
                  {uploadedFile ? (uploadedFile.size / 1024).toFixed(0) : 0} KB • JPEG/PNG
                </p>
              </div>
              
              <button
                type="button"
                id="remove-staged-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  removeStagedFile();
                }}
                className="text-[10px] text-rose-500 hover:text-rose-400 hover:bg-rose-950/20 px-3 py-1.5 rounded border border-transparent hover:border-rose-950 font-bold uppercase tracking-wider transition shrink-0 cursor-pointer"
                title="Remove"
              >
                Remove
              </button>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
