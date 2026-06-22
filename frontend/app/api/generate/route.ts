import { NextRequest, NextResponse } from "next/server";

// Dynamic list of realistic portrait templates for beautiful mockup expression synthesis in AI Studio preview
const PORTRAITS = {
  neutral: [
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&auto=format&fit=crop&q=80", // Female, neutral
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&auto=format&fit=crop&q=80", // Male, neutral
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&auto=format&fit=crop&q=80"  // Female, neutral/slight smile
  ],
  happy: [
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800&auto=format&fit=crop&q=80", // Female, smiley
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&auto=format&fit=crop&q=80", // Female, smiley
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800&auto=format&fit=crop&q=80"  // Male, happy smile
  ],
  angry: [
    "https://images.unsplash.com/photo-1552058544-f2b08422138a?w=800&auto=format&fit=crop&q=80", // Male, frowning/intense
    "https://images.unsplash.com/photo-1542206395-9feb3edaa68d?w=800&auto=format&fit=crop&q=80", // Female, intense expression
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&auto=format&fit=crop&q=80"  // Male, stern/angry
  ],
  surprise: [
    "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=800&auto=format&fit=crop&q=80", // Female, expressive surprise
    "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&auto=format&fit=crop&q=80"  // Male, surprised laugh
  ],
  sad: [
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=800&auto=format&fit=crop&q=80", // Female, melancholic
    "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=800&auto=format&fit=crop&q=80"  // Female, sad neutral
  ],
  disgust: [
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=800&auto=format&fit=crop&q=80", // Male, grimacing
    "https://images.unsplash.com/photo-1489980508314-941910ded1f4?w=800&auto=format&fit=crop&q=80"  // Male, squinted expression
  ],
  fear: [
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=800&auto=format&fit=crop&q=80", // Male, anxious expression
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&auto=format&fit=crop&q=80"  // Female, tensed look
  ]
};

export async function POST(req: NextRequest) {
  try {
    // Parse form data
    const formData = await req.formData();
    const prompt = (formData.get("prompt") as string) || "";
    const selectedFAUsRaw = (formData.get("selectedFAUs") as string) || "[]";
    const uploadedFile = formData.get("uploadedFile") as File | null;

    let selectedFAUs: string[] = [];
    try {
      selectedFAUs = JSON.parse(selectedFAUsRaw);
    } catch (e) {
      selectedFAUs = [];
    }

    // Determine the expression vibe based on prompt and Action Units selected
    const pLower = prompt.toLowerCase();
    let expr: keyof typeof PORTRAITS = "neutral";

    // FACS mapping for simple intelligence
    if (selectedFAUs.includes("AU12") || selectedFAUs.includes("AU6") || pLower.includes("happy") || pLower.includes("smile") || pLower.includes("joy")) {
      expr = "happy";
    } else if (selectedFAUs.includes("AU4") || selectedFAUs.includes("AU23") || selectedFAUs.includes("AU24") || pLower.includes("angry") || pLower.includes("frustrated") || pLower.includes("mad") || pLower.includes("furious")) {
      expr = "angry";
    } else if (selectedFAUs.includes("AU1") && (selectedFAUs.includes("AU15") || selectedFAUs.includes("AU16")) || pLower.includes("sad") || pLower.includes("cry") || pLower.includes("grief") || pLower.includes("depress")) {
      expr = "sad";
    } else if (selectedFAUs.includes("AU26") || selectedFAUs.includes("AU27") || pLower.includes("surprise") || pLower.includes("astonish") || pLower.includes("shock")) {
      expr = "surprise";
    } else if (selectedFAUs.includes("AU9") || selectedFAUs.includes("AU10") || pLower.includes("disgust") || pLower.includes("gross") || pLower.includes("yuck")) {
      expr = "disgust";
    } else if (selectedFAUs.includes("AU20") || pLower.includes("fear") || pLower.includes("scared") || pLower.includes("afraid") || pLower.includes("terror")) {
      expr = "fear";
    }

    // Pick an image from that group
    const group = PORTRAITS[expr];
    // Dynamic index based on prompt key length or a simple randomized seed
    const seed = (prompt.length + selectedFAUs.length) % group.length;
    const selectedImageUrl = group[seed];

    // Simulate synthesis metadata for extreme immersive detail
    const synthesisMetadata = {
      expressionDetected: expr,
      confidence: (0.85 + Math.random() * 0.14).toFixed(3),
      fauCountsApplied: selectedFAUs.length,
      renderingTimeMs: Math.floor(650 + Math.random() * 450),
      timestamp: new Date().toISOString(),
      landmarks: simulateLandmarks(expr, selectedFAUs)
    };

    // Return the response as JSON
    return NextResponse.json({
      success: true,
      image_url: selectedImageUrl,
      metadata: synthesisMetadata
    });

  } catch (error: any) {
    console.error("Synthesizer Route Error:", error);
    return NextResponse.json(
      { success: false, error: error.message || "An error occurred during face expression synthesis simulation." },
      { status: 500 }
    );
  }
}

// Generate coordinate-based landmarks adjusting mock coordinates for SVG rendering on the face
function simulateLandmarks(expr: string, selectedFAUs: string[]) {
  // Base neutral face coordinates inside an SVG container of 400x400
  const baseLandmarks = {
    leftBrow: [ { x: 120, y: 140 }, { x: 140, y: 130 }, { x: 165, y: 135 } ],
    rightBrow: [ { x: 235, y: 135 }, { x: 260, y: 130 }, { x: 280, y: 140 } ],
    leftEye: [ { x: 135, y: 165 }, { x: 150, y: 158 }, { x: 165, y: 165 }, { x: 150, y: 172 } ],
    rightEye: [ { x: 235, y: 165 }, { x: 250, y: 158 }, { x: 265, y: 165 }, { x: 250, y: 172 } ],
    noseBridge: [ { x: 200, y: 150 }, { x: 200, y: 200 } ],
    noseTip: [ { x: 185, y: 220 }, { x: 200, y: 225 }, { x: 215, y: 220 } ],
    mouthOuter: [
      { x: 145, y: 285 }, { x: 175, y: 275 }, { x: 200, y: 278 }, { x: 225, y: 275 }, { x: 255, y: 285 },
      { x: 225, y: 305 }, { x: 200, y: 310 }, { x: 175, y: 305 }
    ],
    jaw: [
      { x: 110, y: 200 }, { x: 115, y: 250 }, { x: 130, y: 300 }, { x: 160, y: 345 },
      { x: 200, y: 365 }, { x: 240, y: 345 }, { x: 270, y: 300 }, { x: 285, y: 250 }, { x: 290, y: 200 }
    ]
  };

  // Adjustments based on FACS
  // AU12 (Smile) -> Pull mouth outward and upward
  if (selectedFAUs.includes("AU12") || expr === "happy") {
    baseLandmarks.mouthOuter[0].x -= 8;
    baseLandmarks.mouthOuter[0].y -= 10;
    baseLandmarks.mouthOuter[4].x += 8;
    baseLandmarks.mouthOuter[4].y -= 10;
    baseLandmarks.mouthOuter[6].y += 5; // deepen jaw line of smile
    baseLandmarks.mouthOuter[2].y -= 4; // slight bow center
  }
  
  // AU15 (Frown) -> Pull mouth corners downward
  if (selectedFAUs.includes("AU15") || expr === "sad") {
    baseLandmarks.mouthOuter[0].y += 12;
    baseLandmarks.mouthOuter[4].y += 12;
    baseLandmarks.mouthOuter[2].y -= 6; // elevate top lip arch center
  }

  // AU1 (Inner brow raiser) -> Pull brows up in the center
  if (selectedFAUs.includes("AU1") || expr === "sad" || expr === "surprise") {
    baseLandmarks.leftBrow[2].y -= 15;
    baseLandmarks.rightBrow[0].y -= 15;
  }

  // AU4 (Brow lowerer) -> Pull brows down and inward
  if (selectedFAUs.includes("AU4") || expr === "angry") {
    baseLandmarks.leftBrow[0].y += 8;
    baseLandmarks.leftBrow[2].y += 12;
    baseLandmarks.leftBrow[2].x += 5;
    baseLandmarks.rightBrow[0].y += 12;
    baseLandmarks.rightBrow[0].x -= 5;
    baseLandmarks.rightBrow[2].y += 8;
  }

  // AU5 (Upper lid raiser) -> Raise eyes
  if (selectedFAUs.includes("AU5") || expr === "surprise" || expr === "fear") {
    baseLandmarks.leftEye[1].y -= 8;
    baseLandmarks.rightEye[1].y -= 8;
  }

  // AU26/AU27 (Jaw Drop / Mouth Stretch) -> Move lower mouth points and chin downward
  if (selectedFAUs.includes("AU26") || selectedFAUs.includes("AU27") || expr === "surprise") {
    const mouthDown = selectedFAUs.includes("AU27") ? 25 : 15;
    baseLandmarks.mouthOuter[5].y += mouthDown;
    baseLandmarks.mouthOuter[6].y += mouthDown + 5;
    baseLandmarks.mouthOuter[7].y += mouthDown;
    baseLandmarks.jaw[4].y += mouthDown * 0.8;
    baseLandmarks.jaw[3].y += mouthDown * 0.6;
    baseLandmarks.jaw[5].y += mouthDown * 0.6;
  }

  return baseLandmarks;
}
