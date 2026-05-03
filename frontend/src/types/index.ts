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
  goal_weight?: number | null;
  gym_id?: number | null;
};

export type ProfileUpdate = Partial<Omit<Profile, "id" | "user_id">>;

// PR — matches backend schemas/pr.py
export type PRCreate = {
  exercise_name: string;
  weight: number;
  reps: number;
};

export type PR = {
  id: number;
  exercise_name: string;
  weight: number;
  reps: number;
  date: string;
  user_id: number;
  user: User;
};

// Exercise catalog — matches backend api/routes/exercises.py
export type ExerciseCatalogEntry = {
  name: string;
  group: string;
};

// Body metrics — matches backend schemas/body_metric.py
export type BodyMetricCreate = {
  weight: number;
  height?: number | null;
  body_fat_pct?: number | null;
};

export type BodyMetric = {
  id: number;
  weight: number;
  height?: number | null;
  body_fat_pct?: number | null;
  date: string;
  user_id: number;
};

// Spot request — matches backend schemas/spot_request.py
export type SpotRequestCreate = {
  spotter_id: number;
};

export type SpotRequest = {
  id: number;
  status: boolean; // true once accepted
  spotter_id: number;
  requester_id: number;
  spotter: User;
  requester: User;
};

// Notification — matches backend schemas/notification.py
export type Notification = {
  id: number;
  message: string;
  type: string;
  time: string; // ISO datetime
  read: boolean;
  user_id: number;
};

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

export type FavoriteExercise={
  id: number;
  name: string;
  user_id: number;
};

// Stats — matches backend schemas/stats.py
export type VolumeStats = {
  total_workouts: number;
  total_sets: number;
  total_reps: number;
  total_volume: number;
  start_date: string;
  end_date: string;
};

export type WorkoutStats = {
  volume: VolumeStats;
  pr_count: number;
  prs: PR[];
};

export type PeriodicVolume = {
  period_start: string;
  total_sets: number;
  total_reps: number;
  total_volume: number;
};
