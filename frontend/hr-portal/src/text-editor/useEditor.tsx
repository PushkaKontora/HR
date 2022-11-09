import React, {useCallback, useMemo, useState} from 'react';
import {BlockType, InlineStyle, KeyCommand} from '../tool-panel/text-editor-block-type';
import {stateToHTML} from './convert';

import {DraftEditorCommand, DraftHandleValue, EditorState, getDefaultKeyBinding, RichUtils} from 'draft-js';
import '../../src/init';

export type EditorApi = {
  state: EditorState;
  onChange: (state: EditorState) => void;
  toggleBlockType: (blockType: BlockType) => void;
  currentBlockType: BlockType;
  hasInlineStyle: (inlineStyle: InlineStyle) => boolean;
  toggleInlineStyle: (inlineStyle: InlineStyle) => void;
  handleKeyCommand: (
    command: KeyCommand,
    editorState: EditorState
  ) => DraftHandleValue;
  handlerKeyBinding: (e: React.KeyboardEvent) => KeyCommand | null;
  toHtml: () => string;
}

export const useEditor = (html?: string): EditorApi => {
  const [state, setState] = useState(() => EditorState.createEmpty());
  const toggleBlockType = useCallback((blockType: BlockType) => {
    setState((currentState) => RichUtils.toggleBlockType(currentState, blockType));
  }, []);

  const currentBlockType = useMemo(() => {
    /* Шаг 1 */
    const selection = state.getSelection();
    /* Шаг 2 */
    const content = state.getCurrentContent();
    /* Шаг 3 */
    const block = content.getBlockForKey(selection.getStartKey());
    /* Шаг 4 */
    return block.getType() as BlockType;
  }, [state]);

  const toggleInlineStyle = useCallback((inlineStyle: InlineStyle) => {
    setState((currentState) => RichUtils.toggleInlineStyle(currentState, inlineStyle));
  }, []);

  const hasInlineStyle = useCallback((inlineStyle: InlineStyle) => {
    /* Получаем иммутабельный Set с ключами стилей */
    const currentStyle = state.getCurrentInlineStyle();
    /* Проверяем содержится ли там переданный стиль */
    return currentStyle.has(inlineStyle);
  }, [state]);

  const handleKeyCommand = useCallback((command: DraftEditorCommand, editorState: EditorState) => {
    const newState = RichUtils.handleKeyCommand(editorState, command);

    if (newState) {
      setState(newState);
      return 'handled';
    }

    return 'not-handled';
  }, []);

  const handlerKeyBinding = useCallback((e: React.KeyboardEvent) => {
    return getDefaultKeyBinding(e);
  }, []);

  const toHtml = React.useCallback(() => {
    return stateToHTML(state.getCurrentContent());
  }, [state]);

  return useMemo(
    () => ({
      state,
      onChange: setState,
      toggleBlockType,
      currentBlockType,
      toggleInlineStyle,
      hasInlineStyle,
      handleKeyCommand,
      handlerKeyBinding,
      toHtml
    }),
    [
      state,
      toggleBlockType,
      currentBlockType,
      toggleInlineStyle,
      hasInlineStyle,
      handleKeyCommand,
      handlerKeyBinding,
      toHtml
    ]
  );
};