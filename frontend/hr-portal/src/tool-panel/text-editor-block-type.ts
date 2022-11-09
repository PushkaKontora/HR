import {DefaultDraftBlockRenderMap, DraftEditorCommand} from 'draft-js';

export enum BlockType {
  /* Список */
  unorderedList = 'unordered-list-item',
  /* Нумерованный список */
  orderList = 'ordered-list-item',
  /* Простой текст */
  default = 'unstyled',
}

export enum InlineStyle {
  BOLD = 'BOLD',
  ITALIC = 'ITALIC',
}

export type KeyCommand = DraftEditorCommand;


