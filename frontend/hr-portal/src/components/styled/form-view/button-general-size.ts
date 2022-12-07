import styled from 'styled-components';
import {LargeMedium} from '../fonts/large';

interface BtnProps {
  padding?: string,
  width?: string,
}

export const ButtonGeneralSize = styled(LargeMedium).attrs<BtnProps>((props) => ({
  padding: (props.padding || '16px 32px'),
  width: (props.width || 'auto'),
}))<BtnProps>`
  padding: ${({padding}) => padding};
  width: ${({width}) => width};
  border-radius: 10px;
  text-align: center;

  &:hover {
    transition: 0.5s;
  }

  &:active {
    box-shadow: inset 0px 2px 10px rgba(0, 0, 0, 0.05);
    transition: 0.5s;
  }
`;
