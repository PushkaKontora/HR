import {Fragment} from 'react';
import {Outlet} from 'react-router-dom';
import Logo from '../../headers/logo/logo';
import styled from 'styled-components';
import Footer from '../../footer/footer';
import {CONTENT_WIDTH} from '../../../const/styled/style-const';
import {useSelector} from 'react-redux';
import {useAppSelector} from '../../../app/hooks';
import {UserStatus} from '../../../types/user-status';

const Main = styled.main`
  min-width: ${CONTENT_WIDTH};
  width: ${CONTENT_WIDTH};
  margin: 0 auto;
  
  flex-grow: 1;
  
  height: 100%;
`;

const Page = styled.div`
  overflow: hidden;
  display: flex;
  flex-direction: column;
  
  min-height: 100vh;
`;

function DefaultLayout() {
  const headerHeight = '120px';
  const status = useAppSelector((state) => state.general.statusUser);
  const showFooter = status !== UserStatus.noAuth;

  return (
    <Page>
      <header style={{height: headerHeight, backgroundColor: '#ddd'}}>
        <Logo></Logo>
      </header>

      <Main>
        <Outlet/>
      </Main>

      {showFooter && <Footer/>}
    </Page>
  );
}

export default DefaultLayout;
