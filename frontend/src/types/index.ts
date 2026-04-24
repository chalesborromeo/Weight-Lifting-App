// Auth — matches backend schemas/auth.py
export type AuthRegister = {
  email: string;
  password: string;
};

export type UserLogin = {
  email: string;
  password: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
  user: User;
};

// User — matches backend schemas/user.py
export type User = {
  id: number;
  email: string;
};

// Profile — matches backend schemas/profile.py
export type Profile = {
  id: number;
  user_id: number;
  first_name?: string | null;
  last_name?: string | null;
  name?: string | null;
  profile_picture_url?: string | null;
  bio?: string | null;
  primary_sport?: string | null;
  location?: string | null;
  state?: string | null;
  gym?: string | null;
  birthdate?: string | null; // ISO date YYYY-MM-DD
  age?: number | null;
  gender?: string | null;
  weight?: number | null;
  gym_id?: number | null;
};

export type ProfileUpdate = Partial<Omit<Profile, "id" | "user_id">>;

// Sets
export type SetCreate = {
  weight: number;
  reps: number;
};

export type Set = {
  id: number;
  weight: number;
  reps: number;
};

// Exercise
export type ExerciseCreate = {
  name: string;
  sets: SetCreate[];
};

export type Exercise = {
  id: number;
  name: string;
  sets: Set[];
};

// Workout
export type WorkoutCreate = {
  user_id: number;
  name: string;
  type: string;
  duration: number;
  exercises: ExerciseCreate[];
};

export type Workout = {
  id: number;
  name: string;
  type: string;
  duration: number;
  exercises: Exercise[];
};

// Post
export type PostCreate = {
  text?: string;
  workout_id?: number;
  club_id?: number;
};

export type Comment = {
  id: number;
  text: string;
  date: string;
  user_id: number;
  user: User;
};

export type Post = {
  id: number;
  date: string;
  text?: string;
  likes: number;
  user_id: number;
  user: User;
  workout_id?: number;
  workout?: Workout;
  club_id?: number;
  comments: Comment[];
};

// Peer
export type Peer = {
  id: number;
  status: string;
  created_at: string;
  user_id: number;
  peer_id: number;
  user: User;
  peer: User;
};

// Club
export type ClubCreate = {
  owner_id: number;
  name: string;
  description?: string;
  privacy: string;
};

export type Club = {
  id: number;
  name: string;
  description?: string;
  owner: User;
  privacy: string;
  members: User[];
};
