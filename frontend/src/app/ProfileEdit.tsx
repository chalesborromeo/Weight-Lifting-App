import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router";
import { profileApi, ApiError, resolveAssetUrl } from "@/api";
import { useCurrentUser } from "@/context/CurrentUser";
import type { Profile, ProfileUpdate } from "@/types";

const SPORTS = ["Running", "Weightlifting", "Cycling", "Swimming", "CrossFit", "Yoga", "Other"];
const GENDERS = ["Man", "Woman", "Non-binary", "Prefer not to say"];

const formatBirthdateLabel = (iso?: string | null) => {
  if (!iso) return "Select Birthdate";
  const d = new Date(iso + "T00:00:00");
  if (Number.isNaN(d.getTime())) return "Select Birthdate";
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
};

export default function ProfileEdit() {
  const navigate = useNavigate();
  const { logout } = useCurrentUser();
  const [form, setForm] = useState<ProfileUpdate>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploadingPicture, setUploadingPicture] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profileExists, setProfileExists] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    (async () => {
      try {
        const p = await profileApi.getMine();
        setForm(stripIdentifiers(p));
        setProfileExists(true);
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          setProfileExists(false);
        } else {
          setError(err instanceof Error ? err.message : "Failed to load profile");
        }
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const update = <K extends keyof ProfileUpdate>(key: K, value: ProfileUpdate[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const handlePictureUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    e.target.value = ""; // allow re-selecting same file later
    if (!file) return;

    if (!profileExists) {
      // Server requires a profile to attach the picture to.
      setError("Save your profile once before uploading a picture.");
      return;
    }

    setUploadingPicture(true);
    setError(null);
    try {
      const updated = await profileApi.uploadPicture(file);
      setForm((prev) => ({ ...prev, profile_picture_url: updated.profile_picture_url }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploadingPicture(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      if (profileExists) await profileApi.update(form);
      else await profileApi.create(form);
      navigate(-1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-10 bg-background/95 backdrop-blur-md">
        <div className="max-w-2xl mx-auto px-6 py-4 flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="text-base text-foreground"
            disabled={saving}
          >
            Cancel
          </button>
          <h1 className="text-base font-semibold">Profile</h1>
          <button
            onClick={handleSave}
            disabled={saving || loading}
            className="text-base text-accent disabled:text-muted-foreground"
          >
            {saving ? "Saving..." : "Save"}
          </button>
        </div>
      </header>

      <main className="max-w-2xl mx-auto pb-12">
        {loading ? (
          <div className="px-6 py-8 text-sm text-muted-foreground">Loading...</div>
        ) : (
          <>
            {/* Identity block: photo + name fields */}
            <section className="px-6 py-4 flex items-center gap-4">
              <Avatar
                url={form.profile_picture_url}
                uploading={uploadingPicture}
                onClick={() => fileInputRef.current?.click()}
              />
              <input
                ref={fileInputRef}
                type="file"
                accept="image/jpeg,image/png,image/webp,image/gif"
                onChange={handlePictureUpload}
                className="hidden"
              />
              <div className="flex-1 bg-card rounded-[15px] divide-y divide-border">
                <input
                  value={form.first_name ?? ""}
                  onChange={(e) => update("first_name", e.target.value)}
                  placeholder="First name"
                  className="w-full bg-transparent px-4 py-3 text-foreground placeholder:text-muted-foreground outline-none"
                />
                <input
                  value={form.last_name ?? ""}
                  onChange={(e) => update("last_name", e.target.value)}
                  placeholder="Last name"
                  className="w-full bg-transparent px-4 py-3 text-foreground placeholder:text-muted-foreground outline-none"
                />
              </div>
            </section>

            {/* Bio + Location group */}
            <Group>
              <TextRow
                value={form.bio ?? ""}
                onChange={(v) => update("bio", v)}
                placeholder="Bio"
              />
              <TextRow
                value={form.location ?? ""}
                onChange={(v) => update("location", v)}
                placeholder="City"
              />
              <TextRow
                value={form.state ?? ""}
                onChange={(v) => update("state", v)}
                placeholder="State"
              />
              <SelectRow
                label="Primary Sport"
                value={form.primary_sport ?? ""}
                onChange={(v) => update("primary_sport", v)}
                options={SPORTS}
              />
            </Group>

            <SectionLabel>ATHLETE INFORMATION</SectionLabel>

            <Group>
              <DateRow
                value={form.birthdate ?? ""}
                onChange={(v) => update("birthdate", v)}
              />
              <SelectRow
                label="Gender"
                value={form.gender ?? ""}
                onChange={(v) => update("gender", v)}
                options={GENDERS}
              />
              <NumberRow
                label="Weight (lbs)"
                value={form.weight ?? null}
                onChange={(v) => update("weight", v)}
                helper="Used to calculate calories, power and more."
              />
            </Group>

            {error && <div className="px-6 py-4 text-sm text-destructive">{error}</div>}

            <div className="px-6 pt-12">
              <button
                type="button"
                onClick={() => {
                  logout();
                  navigate("/");
                }}
                className="w-full text-sm text-destructive py-3"
              >
                Sign out
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

// Strip server-only fields from a Profile so it shapes correctly as ProfileUpdate.
function stripIdentifiers(p: Profile): ProfileUpdate {
  const { id: _id, user_id: _uid, ...rest } = p;
  return rest;
}

function Avatar({
  url,
  uploading,
  onClick,
}: {
  url?: string | null;
  uploading: boolean;
  onClick: () => void;
}) {
  const resolved = resolveAssetUrl(url);
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={uploading}
      aria-label="Change profile picture"
      className="relative w-[60px] h-[60px] rounded-[15px] bg-card overflow-hidden ring-2 ring-accent/80 flex-shrink-0 cursor-pointer hover:opacity-80 transition-opacity"
    >
      {resolved ? (
        <img src={resolved} alt="" className="w-full h-full object-cover" />
      ) : (
        <div className="w-full h-full" />
      )}
      {uploading && (
        <div className="absolute inset-0 bg-black/50 flex items-center justify-center text-white text-xs">
          ...
        </div>
      )}
    </button>
  );
}

function Group({ children }: { children: React.ReactNode }) {
  return (
    <section className="mt-2 bg-card mx-0">
      <div className="divide-y divide-border">{children}</div>
    </section>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="px-6 pt-8 pb-3 text-xs font-semibold tracking-widest text-foreground">
      {children}
    </h2>
  );
}

function TextRow({
  value,
  onChange,
  placeholder,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
}) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full bg-transparent px-6 py-4 text-foreground placeholder:text-muted-foreground outline-none"
    />
  );
}

function SelectRow({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <div className="flex items-center justify-between px-6 py-4">
      <span className="text-foreground">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-transparent text-foreground text-right outline-none cursor-pointer"
      >
        <option value="">—</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}

function DateRow({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <label className="flex items-center justify-between px-6 py-4 cursor-pointer">
      <span className="text-foreground">{formatBirthdateLabel(value)}</span>
      <input
        type="date"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-transparent text-foreground text-right outline-none"
      />
    </label>
  );
}

function NumberRow({
  label,
  value,
  onChange,
  helper,
}: {
  label: string;
  value: number | null;
  onChange: (v: number | null) => void;
  helper?: string;
}) {
  return (
    <div>
      <div className="flex items-center justify-between px-6 py-4">
        <span className="text-foreground">{label}</span>
        <input
          type="number"
          inputMode="decimal"
          value={value ?? ""}
          onChange={(e) => onChange(e.target.value === "" ? null : Number(e.target.value))}
          className="bg-transparent text-foreground text-right outline-none w-24"
        />
      </div>
      {helper && (
        <p className="px-6 pb-4 -mt-2 text-xs text-muted-foreground">{helper}</p>
      )}
    </div>
  );
}
