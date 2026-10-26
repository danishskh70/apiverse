export interface WordDefinition {
  word: string
  phonetic: string
  meanings: {
    partOfSpeech: string
    definitions: {
      definition: string
      example?: string
    }[]
  }[]
  source: string
}

export async function getWordDefinition(
  word: string,
): Promise<WordDefinition> {
  const response = await fetch(
    `/api/v1/integrations/word/definition?word=${encodeURIComponent(word)}`,
  )

  if (!response.ok) {
    throw new Error('Unable to load the word definition. Please try again later.')
  }

  return response.json() as Promise<WordDefinition>
}