import * as React from 'react';
import './tool-panel.scss';
import cn from 'classnames';
import {useEditorApi} from '../text-editor/context';
import {BlockType, InlineStyle} from './text-editor-block-type';

class ToolPanelProps {
}

const INLINE_STYLES_CODES = Object.values(InlineStyle);

export const ToolPanel: React.FC<ToolPanelProps> = ({className}: any) => {

  (window as any).global = window;
  const {
    toggleBlockType,
    currentBlockType,
    toggleInlineStyle,
    hasInlineStyle,
  } = useEditorApi();

  return (
    <div className={cn('tool-panel', className)}>
      <button
        className={cn('tool-panel__item', currentBlockType === BlockType.unorderedList && 'tool-panel__item_active')}
        onMouseDown={(e) => {
          e.preventDefault();
          toggleBlockType(BlockType.unorderedList);
        }}
      >
        Список
      </button>
      <button
        className={cn('tool-panel__item', currentBlockType === BlockType.orderList && 'tool-panel__item_active')}
        onMouseDown={(e) => {
          e.preventDefault();
          toggleBlockType(BlockType.orderList);
        }}
      >
        Список нумерованный
      </button>
      {INLINE_STYLES_CODES.map((code) => {
        const onMouseDown = (e: any) => {
          e.preventDefault();
          toggleInlineStyle(code);
        };

        return (
          <button
            key={code}
            className={cn('tool-panel__item', hasInlineStyle(code) && 'tool-panel__item_active')}
            onMouseDown={onMouseDown}
          >
            {code}
          </button>
        );
      })}

    </div>
  );
};

export default ToolPanel;