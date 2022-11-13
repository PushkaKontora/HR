import styled from 'styled-components';
import {LargeMedium} from '../fonts/large';

export const GrayButton = styled(LargeMedium)`
  background-color: #EDECEA;
  color: black;
  padding: 16px 32px;
  
  border-radius: 10px;
  
  &:disabled {
    background-color: #F6F5F3;
    color: #9C9C9C;
  }
`;
