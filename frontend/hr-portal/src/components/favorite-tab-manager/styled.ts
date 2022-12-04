import styled from 'styled-components';
import {XLargeMedium} from '../styled/fonts/x-large';

export const TabParent = styled(XLargeMedium)`
  display: inline-flex;
  background-color: #F6F5F3;
  border-radius: 10px;
`;

export const Tab = styled.article<{selected: boolean}>`
  margin: 0;
  padding: 24px 40px;
  border-radius: 10px;
  color: ${props => props.selected ? '#000' : '#9C9C9C'};
  background-color: ${props => props.selected ? '#E3EDFF' : '#00000000'};
  
  &:hover {
    background-color: ${props => props.selected ? '#E3EDFF' : '#EDECEA'};
    color: #000;
  }
`;
