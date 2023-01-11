import styled from 'styled-components';
import {XLargeRegular} from '../fonts/x-large';

export const ResumeTitle = styled(XLargeRegular)<{bgColor?: string, padding?: string}>`
  background-color: ${props => props.bgColor || '#F6F5F3'};
  padding: ${props => props.padding || '12px 24px'};
  border-radius: 30px;
  
  display: inline-flex;
  align-items: center;
`;