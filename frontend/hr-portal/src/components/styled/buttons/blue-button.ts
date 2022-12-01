import styled from 'styled-components';
import {LargeMedium} from '../fonts/large';

export const BlueButton = styled(LargeMedium)`
  background-color: #C7DBFF;
  border-radius: 10px;
  padding: 16px 32px;

  &:hover {
    background-color: #E3EDFF;
    transition: 0.5s;
  }

  &:active {
    background-color: #E3EDFF;
    box-shadow: inset 0px 2px 10px rgba(0, 0, 0, 0.05);
    transition: 0.5s;
  }
`;
