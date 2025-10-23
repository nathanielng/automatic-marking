import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

const BEDROCK_LARGE_MODEL_ID = process.env.BEDROCK_LARGE_MODEL_ID || 'global.anthropic.claude-sonnet-4-20250514-v1:0';
const BEDROCK_REGION = process.env.BEDROCK_REGION || 'us-west-2';

const client = new BedrockRuntimeClient({
  region: BEDROCK_REGION,
});

export async function invokeClaude(prompt: string, maxTokens: number = 2048): Promise<string> {
  const messages = {
    role: "user",
    content: [
      {
        type: "text",
        text: prompt
      }
    ]
  };

  const body = {
    messages: [messages],
    max_tokens: maxTokens,
    temperature: 0.5,
    top_k: 250,
    top_p: 1,
    stop_sequences: ["\\n\\nHuman:"],
    anthropic_version: "bedrock-2023-05-31"
  };

  try {
    const command = new InvokeModelCommand({
      modelId: BEDROCK_LARGE_MODEL_ID,
      contentType: "application/json",
      accept: "application/json",
      body: JSON.stringify(body)
    });

    const response = await client.send(command);
    const responseBody = JSON.parse(new TextDecoder().decode(response.body));

    const content = responseBody.content || [];
    const completion = content
      .filter((c: any) => c.type === 'text')
      .map((c: any) => c.text)
      .join('\n');

    return completion || JSON.stringify(responseBody);
  } catch (error) {
    console.error("Error invoking Claude:", error);
    throw error;
  }
}

export async function generateEssayFeedback(
  essayText: string,
  essayName: string,
  rubricText: string,
  feedbackGuidance: string
): Promise<string> {
  const prompt = `You are an expert educator providing detailed feedback on student essays.

<essay>
${essayText}
</essay>

<rubric>
${rubricText}
</rubric>

<feedback_guidance>
${feedbackGuidance}
</feedback_guidance>

Based on the essay, rubric, and feedback guidance provided above, generate comprehensive feedback for this student essay.
Follow the structure and tone guidelines specified in the feedback guidance.

Provide specific band levels, justifications, and actionable recommendations.`;

  console.log(`Generating feedback for essay: ${essayName}`);
  return await invokeClaude(prompt, 3000);
}

export async function generateClassFeedback(
  allFeedbacks: Array<{ name: string; feedback: string }>,
  rubricText: string
): Promise<string> {
  const feedbackSummary = allFeedbacks
    .map(item => `Essay: ${item.name}\n${item.feedback.substring(0, 500)}...`)
    .join("\n\n---\n\n");

  const prompt = `You are an expert educator analyzing overall class performance on an essay assignment.

<rubric>
${rubricText}
</rubric>

<individual_feedbacks>
${feedbackSummary}
</individual_feedbacks>

Based on the rubric and the individual student feedbacks provided above, generate a comprehensive class-level analysis that includes:

1. **Overall Performance Summary**
   - Distribution of band levels across the class
   - General trends and patterns

2. **What Went Well**
   - Common strengths across multiple students
   - Successful application of concepts
   - Positive patterns observed

3. **Areas for Improvement**
   - Common weaknesses or gaps
   - Recurring issues across multiple essays
   - Misconceptions that need addressing

4. **Recommendations for Next Steps**
   - Specific teaching strategies to address common issues
   - Topics that need re-teaching or reinforcement
   - Suggested activities or exercises for the whole class
   - Differentiation strategies for different performance levels

5. **Positive Observations**
   - Growth areas
   - Promising developments
   - Student engagement indicators

Format the response in clear Markdown with appropriate headings and bullet points.`;

  console.log("Generating class overall feedback");
  return await invokeClaude(prompt, 4000);
}
