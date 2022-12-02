import styled from 'styled-components';
import {ButtonGeneralSize} from '../form-view/button-general-size';

export const GrayButton = styled(ButtonGeneralSize)`
  color: #9C9C9C;
  background: #F6F5F3;

  &:hover {
    background: #EDECEA;
    color: #000000;
  }

  &:active {
    background: #EDECEA;
    color: #000000;
  }
`;
