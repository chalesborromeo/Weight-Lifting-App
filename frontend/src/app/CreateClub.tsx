import { useState } from "react";
import { useNavigate } from "react-router";
import { clubsApi } from "@/api";
import { useCurrentUser } from "@/context/CurrentUser";
import { SectionHeader } from "@/components/SectionHeader";

const privacyOptions = ["public", "private"];

export default function CreateClub() {
  const navigate = useNavigate();
  const { userId } = useCurrentUser();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [privacy, setPrivacy] = useState("public");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = name.trim().length > 0 && userId !== null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit || !userId) return;
    setSubmitting(true);
    setError(null);
    try {
      const club = await clubsApi.create({
        name: name.trim(),
        description: description.trim() || undefined,
        privacy,
      });
      navigate(`/clubs/${club.id}`);
    } catch (err) {
      const detail = (err as any)?.body?.detail;
      setError(detail ?? (err instanceof Error ? err.message : "Failed to create club"));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      <SectionHeader title="Create Club" />

      <form onSubmit={handleSubmit} className="bg-card rounded-[20px] p-6 space-y-4">
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground">Club Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Iron Squad"
            className="w-full px-4 py-3 bg-input-background rounded-[15px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent"
            autoFocus
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm text-muted-foreground">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="What's this club about?"
            rows={3}
            className="w-full px-4 py-3 bg-input-background rounded-[15px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-1 focus:ring-accent resize-none"
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm text-muted-foreground">Privacy</label>
          <div className="flex gap-2">
            {privacyOptions.map((opt) => (
              <button
                key={opt}
                type="button"
                onClick={() => setPrivacy(opt)}
                className={`px-4 py-2 text-sm rounded-[15px] capitalize transition-colors ${
                  privacy === opt
                    ? "bg-accent text-white"
                    : "bg-input-background text-muted-foreground hover:text-foreground"
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-sm text-destructive">{error}</p>}

        <button
          type="submit"
          disabled={!canSubmit || submitting}
          className="w-full px-4 py-3 bg-accent text-white rounded-[15px] disabled:opacity-50 hover:bg-accent/90 transition-colors"
        >
          {submitting ? "Creating..." : "Create Club"}
        </button>
      </form>
    </div>
  );
}
