import { createHighlighterCore } from 'shiki/core'
import { createOnigurumaEngine } from 'shiki/engine/oniguruma'

let highlighter = null

const shikiHighlight = async () => {
  if (highlighter) return highlighter

  highlighter = await createHighlighterCore({
    langs: [import('@shikijs/langs/typescript')],
    themes: [import('@shikijs/themes/catppuccin-mocha')],
    engine: createOnigurumaEngine(import('shiki/wasm')),
  })

  return highlighter
}

export const codeToHtml = async (code, lang = 'typescript') => {
  return (await shikiHighlight()).codeToHtml(code, {
    lang,
    theme: 'catppuccin-mocha',
  })
}
