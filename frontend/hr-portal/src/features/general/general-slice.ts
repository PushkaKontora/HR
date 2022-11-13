import {createSlice, isPending} from '@reduxjs/toolkit';
import {UserStatus} from '../../types/user-status';
import {User} from '../../types/user';
import {login} from '../../service/async-actions';
import history from '../../service/browser-history';

interface GeneralState {
  statusUser: UserStatus;
  user: User | null,
  loading: boolean;
  error: string | null;
}


const initialState: GeneralState = {
  statusUser: UserStatus.noAuth,
  user: null,
  loading: false,
  error: null
};

const generalSlice = createSlice({
  name: 'general',
  initialState,
  reducers: {
    indicateStatus(state, action) {
      state.statusUser = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    setError(state, action) {
      state.error = action.payload;
    },
    resetError(state) {
      state.error = null;
    },
    setUser(state, action) {
      state.user = action.payload;
    },
    reset(state) {
      state = initialState;
    }
  }
});

export const {indicateStatus, setLoading, setError, resetError, setUser, reset} = generalSlice.actions;

export default generalSlice.reducer;