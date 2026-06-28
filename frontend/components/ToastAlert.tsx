import React from "react";
import { Sparkles, AlertTriangle } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";

interface ToastAlertProps {
  alertMessage: { type: "success" | "warning" | "error"; text: string } | null;
}

export function ToastAlert({ alertMessage }: ToastAlertProps) {
  return (
    <AnimatePresence>
      {alertMessage && (
        <motion.div
          id="synfer-toast"
          initial={{ opacity: 0, y: -50, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.9 }}
          className={`fixed top-6 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-5 py-3 rounded-xl border shadow-2xl backdrop-blur-md ${
            alertMessage.type === "success" 
              ? "bg-indigo-950/90 border-indigo-500/50 text-indigo-200" 
              : alertMessage.type === "warning"
              ? "bg-zinc-900/90 border-zinc-700/50 text-zinc-300"
              : "bg-rose-950/90 border-rose-500/50 text-rose-200"
          }`}
        >
          {alertMessage.type === "success" && <Sparkles className="w-5 h-5 text-indigo-400 shrink-0" />}
          {alertMessage.type === "warning" && <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />}
          {alertMessage.type === "error" && <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0" />}
          <span className="font-medium text-sm">{alertMessage.text}</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
