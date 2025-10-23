import { NextRequest, NextResponse } from 'next/server';
import { generateClassFeedback } from '@/lib/bedrock';

export async function POST(request: NextRequest) {
  try {
    const { allFeedbacks, rubricText } = await request.json();

    if (!allFeedbacks || !rubricText) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const classFeedback = await generateClassFeedback(allFeedbacks, rubricText);

    return NextResponse.json({ classFeedback });
  } catch (error) {
    console.error('Error generating class feedback:', error);
    return NextResponse.json(
      { error: 'Failed to generate class feedback' },
      { status: 500 }
    );
  }
}
