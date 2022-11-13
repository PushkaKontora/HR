import styled from 'styled-components';
import {LargeRegular} from '../../components/styled/fonts/large';
import {ProfileImage} from '../../components/styled/values/profile-image';


export const ModalButtonContainer = styled.div`
  display: flex;
  flex-wrap: nowrap;
`;

export const Image = styled(ProfileImage)`
  display: inline-block;
  margin-right: 30px;
`;

export const ImageLabel = styled(LargeRegular)`
  display: inline-block;
  
  position: absolute;
  top: 50%;
  transform: translate(0, -50%);

  color: #9C9C9C;
`;
