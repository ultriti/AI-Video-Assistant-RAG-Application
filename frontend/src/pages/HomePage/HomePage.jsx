import { useOutletContext } from "react-router-dom";
import ResultTabs from "../../Components/ResultTabs";
import ChatBox from "../../Components/ChatBox";
import { useApp } from "../../context/AppContext";

const HomePage = () => {
  const { current } = useApp();
  const { loading } = useOutletContext();

  if (!current) {
    return (
      <div className="min-h-[70vh]">
        <section className="border-b border-slate-800/80 pb-6">
          <p className="text-[10px] font-bold tracking-[0.28em] text-violet-300">
            TRANSCRIBE · SUMMARISE · CHAT
          </p>
          <h1 className="mt-3 bg-gradient-to-r from-white via-violet-200 to-indigo-400 bg-clip-text text-4xl font-black tracking-tight text-transparent sm:text-6xl">
            AI Video Assistant
          </h1>
          <p className="mt-3 max-w-xl text-sm leading-6 text-slate-400">
            Turn your meetings into clear summaries, decisions and action items.
            Add a video in the input panel to get started.
          </p>
        </section>
        <div className="mt-7 grid gap-4 sm:grid-cols-3">
          {[
            [
              "01",
              "Transcribe",
              "Convert meeting audio into a searchable transcript.",
            ],
            [
              "02",
              "Understand",
              "Surface the key points, decisions and follow-ups.",
            ],
            [
              "03",
              "Ask anything",
              "Chat with your meeting transcript using AI.",
            ],
          ].map(([number, title, description]) => (
            <article
              key={number}
              className="rounded-xl border border-slate-800 bg-[#101118] p-5"
            >
              <span className="text-xs font-bold tracking-widest text-violet-300">
                {number}
              </span>
              <h2 className="mt-3 text-base font-semibold text-slate-100">
                {title}
              </h2>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                {description}
              </p>
            </article>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-7">
      <section className="border-b border-slate-800/80 pb-5">
        <p className="text-[10px] font-bold tracking-[0.28em] text-slate-500">
          TRANSCRIBE · SUMMARISE · CHAT WITH YOUR MEETINGS
        </p>
        <h1 className="mt-3 bg-gradient-to-r from-white via-violet-200 to-indigo-400 bg-clip-text text-4xl font-black tracking-tight text-transparent sm:text-5xl">
          AI Video Assistant
        </h1>
      </section>
      <ResultTabs result={current} />
      <section className="border-t border-slate-800/80 pt-6">
        <div className="mb-4 flex items-center gap-2">
          <span className="text-lg">💬</span>
          <h2 className="text-lg font-bold text-slate-100">
            Chat with your Meeting
          </h2>
          {loading && (
            <span className="ml-auto text-xs text-amber-300">Analyzing…</span>
          )}
        </div>
        <ChatBox sessionId={current.session_id} />
      </section>
    </div>
  );
};

export default HomePage;
