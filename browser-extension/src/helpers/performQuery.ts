import { Configuration, OpenAIApi } from 'openai';
import { getValueFromStorage, SELECTED_OPENAI_MODEL } from '../state';

const systemMessage = `
You are a browser automation assistant.

You can use the following tools:

1. click(elementId: number): clicks on an element
2. setValue(elementId: number, value: string): sets the value of an element

You should show your work in the following format:

Thought 1: I think I should...
Action 1: click(...) or setValue(...)

Only perform one action per block
`;

export async function performQuery(
  instructions: string,
  simplifiedDOM: string
) {
  const model = (await getValueFromStorage(
    SELECTED_OPENAI_MODEL,
    'gpt-3.5-turbo'
  )) as string;
  const prompt = formatPrompt(instructions, simplifiedDOM);
  const openai = new OpenAIApi(
    new Configuration({
      apiKey: (await chrome.storage.sync.get('openai-key'))['openai-key'],
    })
  );

  try {
    const completion = await openai.createChatCompletion({
      model: model,
      messages: [
        {
          role: 'system',
          content: systemMessage,
        },
        { role: 'user', content: prompt },
      ],
      max_tokens: 500,
    });
    console.log('completion', completion);

    return completion.data.choices[0].message?.content?.trim() || '';
  } catch (error: any) {
    throw new Error(model + error.response.data.error.message);
  }
}

export function formatPrompt(instructions: string, simplifiedDOM: string) {
  return `You are on a page with the following simplified DOM structure:
  
\`\`\`
${simplifiedDOM}
\`\`\`

The user requests the following task:

${instructions}`;
}