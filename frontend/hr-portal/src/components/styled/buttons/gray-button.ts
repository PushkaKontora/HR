import styled from 'styled-components';
import {LargeMedium} from '../fonts/large';

export const GrayButton = styled(LargeMedium)`
  padding: 16px 32px;
  color: #9C9C9C;
  background: #F6F5F3;

  border-radius: 10px;

  &:hover {
    background: #EDECEA;
    color: #000000;
    transition: 0.5s;
  }

  &:active {
    box-shadow: inset 0px 2px 10px rgba(0, 0, 0, 0.05);
    background: #EDECEA;
    color: #000000;
    transition: 0.5s;
  }
`;
