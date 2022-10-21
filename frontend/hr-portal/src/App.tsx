import './App.css';

import {incremented} from './features/example/example-slice';
import {useAppDispatch, useAppSelector} from './app/hooks';

function App() {
  const count = useAppSelector((state) => state.example.valueCount);
  const dispatch = useAppDispatch();

  const handlerClick = () => {
    dispatch(incremented());
  };
  return (
    <div className="App">
      <div>
        <a href="https://vitejs.dev" target="_blank" rel="noreferrer">
          <img src="/vite.svg" className="logo" alt="Vite logo"/>
        </a>
        <a href="https://reactjs.org" target="_blank" rel="noreferrer">
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={handlerClick}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  );
}

export default App;
