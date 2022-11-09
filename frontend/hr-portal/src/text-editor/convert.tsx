import {convertToHTML} from 'draft-convert';
import {BlockType, InlineStyle} from '../tool-panel/text-editor-block-type';

export const stateToHTML = convertToHTML({
  styleToHTML: (style) => {
    switch (style) {
    case InlineStyle.BOLD:
      return <strong/>;
    default:
      return null;
    }
  },
  blockToHTML: (block) => {
    switch (block.type) {
    case BlockType.default:
      return <p/>;
    default:
      return null;
    }
  },
});