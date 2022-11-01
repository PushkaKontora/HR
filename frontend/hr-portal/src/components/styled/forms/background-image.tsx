import styled from 'styled-components';
import bg from '../../../assets/svg/login-bg.svg';
import {CONTENT_WIDTH} from '../../../const/styled/style-const';

export const ParentForBackgroundImage = styled.div`
  width: ${CONTENT_WIDTH};
  position: absolute;
  bottom: 0;
  z-index: -999;
`;

export const BackgroundImage = styled.div`
  margin-left: auto;
  
  background-image: url(${bg});
  background-repeat: no-repeat;
  
  width: 568px;
  height: 568px;
`;