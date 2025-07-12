import sys
import os
from pathlib import Path
# Add project root to Python path
project_root = str(Path(__file__).parent)
sys.path.append(project_root)

import logging
from typing import List, Optional
from engine.scroll_runner import ScrollRunner
from engine.fork_evaluator import ForkEvaluator
from engine.mirror_protocol import MirrorProtocol
from engine.certifier import Certifier
from modules.compliance_type.ethical import EthicalCompliance
from modules.compliance_type.regulatory import RegulatoryCompliance
from modules.compliance_type.risk import RiskCompliance
from modules.target_type.process import ProcessTarget
from modules.target_type.system import SystemTarget
from modules.industry.banking import BankingIndustry
from modules.industry.insurance import InsuranceIndustry
from modules.industry.health import HealthIndustry
from modules.regulations.gdpr import GDPRRule
from modules.regulations.hipaa import HIPAARule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main(org: str = "Example Corp", target_type: str = "process") -> None:
    try:
        # Validate inputs
        if not org or not isinstance(org, str):
            raise ValueError("Organization name must be a non-empty string")
        if target_type not in ["process", "system"]:
            raise ValueError("Target type must be 'process' or 'system'")

        # Instantiate target
        if target_type == "process":
            target = ProcessTarget("Onboarding")
        else:
            target = SystemTarget("CoreSystem")
        context = target.get_context()
        if context is None:
            raise ValueError(f"Failed to retrieve context from {target_type.capitalize()}Target")

        # Compliance types
        compliance_results = {}
        compliance_types = [
            (EthicalCompliance, ["onboarding_consent", "data_minimization"], "Ethical"),
            (RegulatoryCompliance, ["onboarding_consent"], "Regulatory"),
            (RiskCompliance, ["automated_profiling"], "Risk")
        ]

        for compliance_class, rules, name in compliance_types:
            try:
                compliance = compliance_class(rules=rules)
                result = compliance.evaluate(context)
                compliance_results[name] = result
                logger.info(f"{name} compliance evaluation completed: {result}")
            except Exception as e:
                logger.error(f"Error evaluating {name} compliance: {e}")
                raise

        # Industry forks
        industries = [
            (BankingIndustry(), "Banking"),
            (HealthIndustry(), "Health"),
            (InsuranceIndustry(), "Insurance")
        ]
        all_forks = []
        for industry, name in industries:
            if not hasattr(industry, "forks"):
                raise AttributeError(f"{name}Industry does not have 'forks' attribute")
            all_forks.extend(industry.forks)

        # Regulation scrolls
        regulations = [
            (GDPRRule(), "GDPR"),
            (HIPAARule(), "HIPAA")
        ]
        scrolls = []
        for regulation, name in regulations:
            if not hasattr(regulation, "scroll"):
                raise AttributeError(f"{name}Rule does not have 'scroll' attribute")
            scrolls.append(regulation.scroll)

        # Run scrolls
        scroll_results = ScrollRunner(scrolls).run_scrolls(context)
        if not scroll_results:
            logger.warning("No scrolls were processed successfully")

        # Evaluate forks
        fork_results = ForkEvaluator(all_forks).evaluate_forks(context)
        if not fork_results:
            logger.warning("No forks were evaluated successfully")

        # Reflect
        reflection = MirrorProtocol().reflect(scroll_results, fork_results)
        logger.info("Reflection completed")

        # Ensure output directory exists
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)
        cert_path = output_dir / f"certification_report_{org}_{target_type}.pdf"

        # Certify
        certifier = Certifier(str(cert_path))
        cert_path = certifier.generate_report(org, scroll_results, fork_results, reflection, compliance_results)
        logger.info(f"Certification generated: {cert_path}")

    except Exception as e:
        logger.error(f"Error in compliance evaluation process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run compliance evaluation for an organization")
    parser.add_argument("--org", default="Example Corp", help="Organization name")
    parser.add_argument("--target-type", default="process", choices=["process", "system"], help="Target type (process or system)")
    args = parser.parse_args()
    main(args.org, args.target_type)