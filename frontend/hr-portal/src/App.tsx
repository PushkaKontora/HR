import './App.css';

import {incremented} from './features/example/example-slice';
import {useAppDispatch, useAppSelector} from './app/hooks';
import Header from './components/header/header';
import Footer from './components/footer/footer';
import JobSearchScreen from './pages/job-search-screen/job-search-screen';

function App() {
  const count = useAppSelector((state) => state.example.valueCount);
  const dispatch = useAppDispatch();

  const handlerClick = () => {
    dispatch(incremented());
  };
  return (
    <div className="App">
      <Header/>
      <JobSearchScreen/>
      <Footer/>

    </div>
  );
}

export default App;
