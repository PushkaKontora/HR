import {createSlice} from '@reduxjs/toolkit';
import {UserStatus} from '../../types/user-status';
import {User} from '../../types/user';
import {
  deleteUserPhoto,
  loadUserPhoto, resetPassword,
  updateEmailAction,
  updateName
} from '../../service/async-actions/async-actions-profile';
import {Competency} from '../../types/competency';
import {getCompetenciesAction} from '../../service/async-actions/async-actions-competencies';
import {deleteUser} from '../../service/async-actions/async-actions-delete-user';

interface GeneralState {
  statusUser: UserStatus;
  user: User | null,
  loading: boolean;
  error: string | null;
  competencies: Competency[]
}

const initialState: GeneralState = {
  statusUser: UserStatus.noAuth,
  user: null,
  loading: false,
  error: null,
  competencies: []
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
    },
    setCompetencies(state, action) {
      state.competencies = action.payload;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(updateEmailAction.fulfilled, (state, action) => {
        if (state.user) {
          state.user.email = action.payload;
        }
      })
      .addCase(updateName.fulfilled, (state, action) => {
        if (state.user) {
          state.user.name = action.payload.name;
          state.user.surname = action.payload.surname;
          state.user.patronymic = action.payload.patronymic;
        }
      })
      .addCase(loadUserPhoto.fulfilled, (state, action) => {
        if (state.user) {
          state.user.photo = action.payload;
        }
      })
      .addCase(deleteUserPhoto.fulfilled, (state) => {
        if (state.user) {
          state.user.photo = '';
        }
      })
      .addCase(resetPassword.fulfilled, (state, action) => {
        if (state.user) {
          state.user.password = action.payload;
        }
      })
      .addCase(getCompetenciesAction.fulfilled, (state, action) => {
        state.competencies = action.payload;
      })
      .addCase(deleteUser.fulfilled, (state) => {
        state.user = null;
        state.statusUser = UserStatus.noAuth;
      });
  }
});

export const {indicateStatus, setLoading, setError, resetError, setUser, reset} = generalSlice.actions;

export default generalSlice.reducer;