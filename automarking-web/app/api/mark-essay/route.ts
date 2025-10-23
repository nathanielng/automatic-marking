import { NextRequest, NextResponse } from 'next/server';
import { generateEssayFeedback } from '@/lib/bedrock';

export async function POST(request: NextRequest) {
  try {
    const { essayText, essayName, rubricText, feedbackGuidance } = await request.json();

    if (!essayText || !essayName || !rubricText || !feedbackGuidance) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const feedback = await generateEssayFeedback(
      essayText,
      essayName,
      rubricText,
      feedbackGuidance
    );

    return NextResponse.json({ feedback });
  } catch (error) {
    console.error('Error marking essay:', error);
    return NextResponse.json(
      { error: 'Failed to generate feedback' },
      { status: 500 }
    );
  }
}
