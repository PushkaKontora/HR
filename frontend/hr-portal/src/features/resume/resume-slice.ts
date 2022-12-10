import {createSlice} from '@reduxjs/toolkit';

import {getCompetenciesAction} from '../../service/async-actions/async-actions-competencies';
import {getResumeList} from '../../service/async-actions/async-actions-resume';
import {ResumeList} from '../../types/resume-list';

export interface CompetenciesOption {
  readonly value: string;
  readonly label: string;
}

interface ResumeState {
  competenciesApi: CompetenciesOption[];
  resumeList: ResumeList | null;
}

const initialState: ResumeState = {
  competenciesApi: [],
  resumeList: null,
};

const resumeSlice = createSlice({
  name: 'resume-slice',
  initialState,
  reducers: {},
  extraReducers(builder) {
    builder
      .addCase(getCompetenciesAction.fulfilled, (state, action) => {
        const viewCompetence = action.payload.map((competence): CompetenciesOption => {
          return {value: competence.name, label: competence.name};
        });
        state.competenciesApi = viewCompetence;
      })
      .addCase(getResumeList.fulfilled, (state, action) => {
        state.resumeList = action.payload;
        console.log(action.payload, 'action.payload');
        console.log(action.payload, 'action.payload');
      });
  }
});

// export const {} = resumeSlice.actions;

export default resumeSlice.reducer;